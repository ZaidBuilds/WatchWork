import { getStoredUser } from "./api";

export function getTokenFromStorage(): string | null {
  return getStoredUser()?.access_token ?? null;
}
