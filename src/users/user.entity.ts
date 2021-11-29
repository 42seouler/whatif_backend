import { Column, Entity, PrimaryGeneratedColumn } from 'typeorm';
import { UserRole } from '../enums/user.role.enum';
import { BaseCommonEntity } from '../common/base-common.entity';

@Entity()
export class User extends BaseCommonEntity {
  @Column()
  email: string;

  @Column()
  password: string;

  @Column({
    type: 'enum',
    enum: UserRole,
    default: UserRole.USER,
  })
  roles: UserRole[];
}
