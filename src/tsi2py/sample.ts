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

console.log("hello world");

const func = () => {
  console.log("hello world");
};

const list = [1, 2, 3];

console.log(list.map((x) => x * 2));

const user: User = {
  id: 1,
  username: "danny",
  email: "danny@example.com",
  isActive: true,
  createdAt: new Date(),
};
