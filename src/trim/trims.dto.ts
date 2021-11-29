import { IsNumber, IsString } from "class-validator";

export class TrimsDto {
  @IsString()
  id: string;
  @IsNumber()
  trimId: number;
}
