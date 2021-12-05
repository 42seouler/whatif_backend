from typing import Optional, List
from fastapi import FastAPI, Header, HTTPException
from sqlmodel import Session, select
from entities.company import Company
from entities.company_translation import CompanyTranslation
from entities.locales import Locales
from entities.tag import Tag
from entities.tag_translation import TagTranslation
from entities.company_tag import CompanyTag
from dtos.request_dto import RequestDto
from dtos.response_dto import ResponseDto
from utils.database import engine, create_db_and_tables
from insert_temp_data import save_db

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    save_db()


@app.get("/search")
async def company_name_autocomplete(query: str, x_wanted_language: Optional[List[str]] = Header(None)):
    if query == "":
        raise HTTPException(status_code=404, detail="검색어를 입력하세요.")
    company_name_list = []
    with Session(engine) as session:
        # 지역을 찾는다
        statement = select(Locales).where(Locales.name == x_wanted_language[0])
        results = session.exec(statement)
        existed_locale = results.first()
        if not existed_locale:
            raise HTTPException(status_code=404, detail="존재하지 않는 지역입니다.")
        # 지역에 해당하는 회사를 찾는다 (Sqlmodel에서 지원하는 like를 찾지 못했음)
        statement = select(CompanyTranslation).where(CompanyTranslation.locales_id == existed_locale.id)
        results = session.exec(statement).fetchall()
        print(results)
        for result in results:
            if query in result.name:
                company_name_list.append({
                    "company_name": result.name
                })
    return company_name_list


@app.get("/companies/{company_name}")
async def company_search(company_name: str, x_wanted_language: Optional[List[str]] = Header(None)):
    search_company_name = ""
    tags = []
    with Session(engine) as session:
        # 같은 이름을 갖고 있는 회사를 찾는다.
        statement = select(CompanyTranslation).where(CompanyTranslation.name == company_name)
        results = session.exec(statement)
        existed_company = results.first()

        if not existed_company:
            raise HTTPException(status_code=404, detail="존재하지 않는 회사명입니다.")

        # 회사가 존재하면 결과값을 생성
        statement = select(Locales).where(Locales.name == x_wanted_language[0])
        results = session.exec(statement)
        existed_locale = results.first()
        statement = select(CompanyTranslation).where(
            CompanyTranslation.company_id == existed_company.company_id, CompanyTranslation.locales_id == existed_locale.id)
        results = session.exec(statement)
        search_company = results.first()
        search_company_name = search_company.name

        # 회사가 갖고 있는 태그를 찾음
        statement = select(CompanyTag).where(CompanyTag.company_id == existed_company.company_id)
        company_tags = session.exec(statement).fetchall()
        for company_tag in company_tags:
            statement = select(TagTranslation).where(
                TagTranslation.locales_id == existed_locale.id, TagTranslation.tag_id == company_tag.tag_id)
            results = session.exec(statement)
            tag = results.first()
            tags.append(tag.name)

    return ResponseDto(company_name=search_company_name, tags=tags)


@app.post("/companies")
async def create_company(request: RequestDto, x_wanted_language: Optional[List[str]] = Header(None)):
    # 생성과 동시에 응답값 생성을 위한 변수들
    result_company_name = ""
    tags = []
    with Session(engine) as session:
        # 회사명이 존재한다면 에러 처리
        for _, name in request.company_name.items():
            statement = select(CompanyTranslation).where(CompanyTranslation.name == name)
            results = session.exec(statement)
            existed_name = results.first()
            if existed_name:
                raise HTTPException(status_code=400, detail="이미 존재하는 회사명입니다.")
        # 회사 생성
        company = Company()
        session.add(company)
        session.commit()
        # 지역정보, 회사이름으로 지역 별 회사 이름 생성
        for locale, company_name in request.company_name.items():
            statement = select(Locales).where(Locales.name == locale)
            results = session.exec(statement)
            existed_locale = results.first()
            if existed_locale:
                new_company_translation = CompanyTranslation(
                    company_id=company.id, locales_id=existed_locale.id, name=company_name)
                session.add(new_company_translation)
            else:
                new_locales = Locales(name=locale)
                session.add(new_locales)
                session.commit()
                new_company_translation = CompanyTranslation(
                    company_id=company.id, locales_id=new_locales.id, name=company_name)
                session.add(new_company_translation)
            # 요쳥 된 로케일의 값이라면
            if locale == x_wanted_language[0]:
                result_company_name = company_name
        session.commit()
        # 태그 생성
        for tag in request.tags:
            # 태그 List[dict]에서 한개의 딕셔너리를 선택
            tag_list = list(tag.values())[0]

            # 오리지널 테그 확인
            origin_tag = list(tag_list.values())[0]
            origin_tag_name = origin_tag.split('_')[-1]
            statement = select(Tag).where(Tag.name == origin_tag_name)
            results = session.exec(statement)
            existed_origin_tag = results.first()

            # 오리지널 태그가 존재하지 않으면 생성
            if not existed_origin_tag:
                new_origin_tag = Tag(name=origin_tag_name)
                session.add(new_origin_tag)
                session.commit()
                existed_origin_tag = new_origin_tag

            # 지역별 태그
            for lo, ta in tag_list.items():
                #  지역을 찾는다.
                locale = select(Locales).where(Locales.name == lo)
                results = session.exec(locale)
                existed_locale = results.first()

                # 지역에 해당 태그가 있는지 확인
                statement = select(TagTranslation).where(
                    TagTranslation.name == ta, TagTranslation.locales_id == existed_locale.id)
                results = session.exec(statement)
                existed_tag = results.first()

                # 태그가 없으면
                if not existed_tag:
                    new_tag_translation = TagTranslation(
                        tag_id=existed_origin_tag.id, locales_id=existed_locale.id, name=ta)
                    session.add(new_tag_translation)

                # 요청한 로케일 정보와 일치하는 태그 목록 생성
                if lo == x_wanted_language[0]:
                    tags.append(ta)
            #회사의 태그 목록 생성
            new_company_tag = CompanyTag(tag_id=existed_origin_tag.id, company_id=company.id)
            session.add(new_company_tag)

        session.commit()
        return ResponseDto(company_name=result_company_name, tags=tags)
