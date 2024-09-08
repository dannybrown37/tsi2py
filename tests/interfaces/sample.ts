interface User {
  id: number;
  username: string;
  email: string;
  isActive: boolean;
  createdAt: Date;
}

interface Product {
  id: string;
  name: string;
  price: number;
  tags: string[];
  available: boolean;
}

interface Order {
  orderId: number;
  userId: number;
  products: Product[];
  totalAmount: number;
  orderDate: Date;
}

interface APIResponse<T> {
  data: T;
  success: boolean;
  message: string;
}

interface Config {
  env: "development" | "production" | "test";
  debug: boolean;
  version: number;
  paths: {
    logs: string;
    temp: string;
  };
  maxRetries: number | null;
}
