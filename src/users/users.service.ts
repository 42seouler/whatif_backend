import {
  ForbiddenException,
  Injectable,
  NotFoundException,
} from '@nestjs/common';
import { CreateUserDto } from './dto/create-user.dto';
import { UsersRepository } from './users.repository';
import { UpdateUserDto } from './dto/update-user-dto';
import { User } from './user.entity';
import * as bcrypt from 'bcrypt';
import { classToPlain, plainToClass } from 'class-transformer';
import { ReadUserDto } from './dto/read-user-dto';

@Injectable()
export class UsersService {
  constructor(private readonly usersRepository: UsersRepository) {}
  async findByEmail(email: string): Promise<User> {
    return await this.usersRepository.findOne({
      email: email,
    });
  }

  async create(createUserDto: CreateUserDto): Promise<number> {
    const existingUser = await this.usersRepository.findOne({
      email: createUserDto.email,
    });
    if (existingUser) {
      throw new ForbiddenException();
    }
    const hash = await bcrypt.hash(createUserDto.password, 10);
    const user = this.usersRepository.create({
      ...createUserDto,
      password: hash,
    });
    const userPromise = await this.usersRepository.save(user);
    return userPromise.id;
  }

  async findAll() {
    return this.usersRepository.find();
  }

  async findOne(id: number): Promise<User> {
    const existingUser = await this.usersRepository.findOne({
      id: id,
    });
    if (!existingUser) {
      throw new NotFoundException();
    }
    return existingUser;
  }

  async update(id: number, updateUserDto: UpdateUserDto): Promise<ReadUserDto> {
    const existingUser = await this.usersRepository.findOne({
      id: id,
    });
    if (!existingUser) {
      throw new NotFoundException();
    }
    existingUser.password = await bcrypt.hash(updateUserDto.password, 10);
    const updateUser = await this.usersRepository.save(existingUser);
    return plainToClass(ReadUserDto, classToPlain(updateUser), {
      excludeExtraneousValues: true,
    });
  }

  async remove(id: number): Promise<number> {
    const existingUser = await this.usersRepository.findOne({
      id: id,
    });
    if (!existingUser) {
      throw new NotFoundException();
    }
    await this.usersRepository.remove(existingUser);
    return id;
  }
}
