import { Body, Controller, Post } from "@nestjs/common";
import { TrimService } from "./trim.service";
import { CreateUserDto } from "../users/dto/create-user.dto";
import { TrimsDto } from "./trims.dto";
import { TrimListDto } from "./TrimListDto";

@Controller('trims')
export class TrimsController {
  constructor(private readonly trimService: TrimService) {}

  @Post()
  create(@Body() createUserDto: TrimListDto) {
    // return this.trimService.create(createUserDto);
    console.log(createUserDto);
  }
}
