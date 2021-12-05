from sqlmodel import Session, select
from entities.company import Company
from entities.company_translation import CompanyTranslation
from entities.locales import Locales
from entities.tag import Tag
from entities.tag_translation import TagTranslation
from entities.company_tag import CompanyTag
import csv
from utils.database import engine


def save_db():
    f = open("wanted_temp_data.csv", "r", encoding='utf-8')
    rdr = list(csv.reader(f))
    with Session(engine) as session:
        # 지역 추가
        locale_list = []
        locale_ko = Locales(name="ko")
        locale_en = Locales(name="en")
        locale_ja = Locales(name="ja")
        session.add(locale_ko)
        session.add(locale_en)
        session.add(locale_ja)
        session.commit()

        # 편의를 위한 배열
        locale_list.append(locale_ko)
        locale_list.append(locale_en)
        locale_list.append(locale_ja)

        # 회사 별 저장
        for csv_company in rdr[1:]:
            # 회사 생성
            company = Company()
            session.add(company)
            session.commit()
            # 회사의 요소를 순회
            for index, element in enumerate(csv_company):
                if index < 3 and element != "":
                    company_translation = CompanyTranslation(company_id=company.id,
                                                             locales_id=locale_list[index % 3].id, name=element)
                    session.add(company_translation)
                elif element != "":
                    # 로케일 단위의 태그를 리스트로 변환
                    split_tags = element.split('|')
                    for tag in split_tags:
                        origin_tag = tag.split('_')[-1]
                        statement = select(Tag).where(Tag.name == origin_tag)
                        results = session.exec(statement)
                        existed_origin_tag = results.first()

                        # 오리지널 태그가 존재하지 않으면 생성
                        if not existed_origin_tag:
                            new_origin_tag = Tag(name=origin_tag)
                            session.add(new_origin_tag)
                            session.commit()
                            existed_origin_tag = new_origin_tag

                        tag_translation = TagTranslation(tag_id=existed_origin_tag.id,
                                                         locales_id=locale_list[index % 3].id, name=tag)
                        session.add(tag_translation)
                        # 회사가 태그를 갖고 있지 않다면
                        statement = select(CompanyTag).where(CompanyTag.tag_id == existed_origin_tag.id,
                                                             CompanyTag.company_id == company.id)
                        results = session.exec(statement)
                        existed_company = results.first()
                        if not existed_company:
                            new_company_tag = CompanyTag(tag_id=existed_origin_tag.id, company_id=company.id)
                            session.add(new_company_tag)
                        session.commit()
    f.close()
