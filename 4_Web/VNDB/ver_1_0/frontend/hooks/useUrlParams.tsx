import { useRouter, usePathname, useSearchParams } from "next/navigation";

export const useUrlParams = () => {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const removeKey = (key: string) => {
    const params = new URLSearchParams(searchParams);
    params.delete(key);
    router.push(`${pathname}?${params.toString()}`);
  }

  const removeMultipleKeys = (keys: string[]) => {
    const params = new URLSearchParams(searchParams);
    keys.forEach(key => params.delete(key));
    router.push(`${pathname}?${params.toString()}`);
  }

  const updateKey = (key: string, value: string) => {
    const params = new URLSearchParams(searchParams);
    params.set(key, value);
    router.push(`${pathname}?${params.toString()}`);
  }

  const updateMultipleKeys = (params: Record<string, string>) => {
    const newParams = new URLSearchParams(searchParams);
    Object.entries(params).forEach(([key, value]) => {
      newParams.set(key, value);
    });
    router.push(`${pathname}?${newParams.toString()}`);
  }

  const clearKeys = () => {
    router.push(pathname);
  }

  return { 
    removeKey, removeMultipleKeys, 
    updateKey, updateMultipleKeys, 
    clearKeys
  };
}