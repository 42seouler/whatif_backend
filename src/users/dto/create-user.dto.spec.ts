import {
  ArgumentMetadata,
  BadRequestException,
  ValidationPipe,
} from '@nestjs/common';
import { CreateUserDto } from './create-user.dto';

describe('ValidationPipe', () => {
  let target: ValidationPipe;
  const metadata: ArgumentMetadata = {
    type: 'body',
    metatype: CreateUserDto,
    data: '',
  };

  describe('transform', () => {
    describe('when validation pass', () => {
      it('should return a CreateUserDto instance', async () => {
        target = new ValidationPipe({ transform: true });
        const testObj = { email: 'wanted@wanted.com', password: '0123456789' };
        expect(await target.transform(testObj, metadata)).toBeInstanceOf(
          CreateUserDto,
        );
      });
    });

    describe('when validation fails', () => {
      beforeEach(() => {
        target = new ValidationPipe();
      });
      it('should throw an error if email is not define', async () => {
        const testObj = { password: '0123456789' };
        await expect(target.transform(testObj, metadata)).rejects.toThrow(
          BadRequestException,
        );
      });
      it('should throw an error if email format is incorrect', async () => {
        const testObj = { email: 'watend', password: '0123456789' };
        await target
          .transform(testObj, metadata)
          .catch((error) =>
            expect(error.getResponse().message).toEqual([
              'email must be an email',
            ]),
          );
      });
      it('should throw an error if password is not define', async () => {
        const testObj = { email: 'wanted@wecode.com' };
        await expect(target.transform(testObj, metadata)).rejects.toThrow(
          BadRequestException,
        );
      });
      it('should throw an error if password is less than 10 characters', async () => {
        const testObj = { email: 'wanted@wecode.com', password: '012345678' };
        try {
          await target.transform(testObj, metadata);
        } catch (error) {
          expect(error.getResponse().message).toEqual([
            'password must be at least 10 characters',
          ]);
        }
      });
    });
  });
});
