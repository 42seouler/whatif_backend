import { Column, Entity, PrimaryColumn, PrimaryGeneratedColumn } from "typeorm";

@Entity()
export class Trims {
  @PrimaryGeneratedColumn()
  primary: number;

  @Column()
  id: string;

  @Column()
  trimId: number;
}
