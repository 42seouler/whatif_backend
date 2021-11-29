import { TrimsDto } from "./trims.dto";
import { IsArray } from "class-validator";

export class TrimListDto {
  @IsArray()
  trimList: TrimsDto;
}