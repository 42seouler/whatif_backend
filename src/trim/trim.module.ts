import { Module } from '@nestjs/common';
import { TrimService } from './trim.service';
import { AppController } from "../app.controller";
import { TrimsController } from "./trims.controller";

@Module({
  providers: [TrimService],
  controllers: [TrimsController],
})
export class TrimModule {}
