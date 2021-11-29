import { Injectable } from '@nestjs/common';

@Injectable()
export class AppService {
  getHello(): string {
    return '개인 사정으로 인해 젠킨스 CICD만 구현하였습니다. 죄송합니다 ㅠ0ㅜ';
  }
}
