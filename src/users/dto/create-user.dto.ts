import { IsEmail, IsNotEmpty, MinLength } from 'class-validator';
import { ApiProperty } from '@nestjs/swagger';
import { Expose } from 'class-transformer';

export class CreateUserDto {
  @IsEmail()
  @Expose()
  @ApiProperty()
  email: string;

  @IsNotEmpty()
  @MinLength(10, {
    message: 'password must be at least 10 characters',
    context: {
      errorCode: 1003,
      developerNote: 'The validated string must contain 10 or more characters.',
    },
  })
  @ApiProperty()
  password: string;
}
