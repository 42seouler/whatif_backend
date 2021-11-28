import { Test, TestingModule } from '@nestjs/testing';
import { UsersController } from './users.controller';
import { UsersService } from './users.service';
import { CreateUserDto } from './dto/create-user.dto';
import { ReadUserDto } from './dto/read-user-dto';
import { create } from 'domain';

jest.mock('./users.service');

describe('UsersController', () => {
  let controller: UsersController;
  let service: UsersService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [UsersService],
      controllers: [UsersController],
    }).compile();

    controller = module.get<UsersController>(UsersController);
    service = module.get<UsersService>(UsersService);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });

  describe('user is created', () => {
    describe('when user is generated', () => {
      it('should be called service-create-method', () => {
        const request = {} as CreateUserDto;
        controller.create(request);
        expect(service.create).toBeCalled();
      });
      it('should return the value readUserDto', () => {
        // given
        const request = {
          email: 'wanted@wecode.com',
          password: '0123456789',
        };
        const response = {
          ...request,
        } as ReadUserDto;
        // when
        controller.create(request);
      });
    });

    describe('when user is not generated', () => {
      it('should return the value readUserDto', () => {
        const request = {
          email: 'wanted@wecode.com',
          password: '0123456789',
        };
        controller.create(request);
        expect(service.create).toBeCalled();
      });
    });
  });
});
