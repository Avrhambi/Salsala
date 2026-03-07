import { User } from "../../common/types";
import { UserSchema } from "../../common/validation";
import { apiClient } from "./client";

export async function createUser(displayName: string): Promise<User> {
  const { data } = await apiClient.post("/user/create", { display_name: displayName });
  return UserSchema.parse(data);
}
