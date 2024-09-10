enum Status {
  Active = "ACTIVE",
  Inactive = "INACTIVE",
  Suspended = "SUSPENDED",
}

interface User {
  id: number;
  name: string;
  status: Status;
  lastLogin: Date;
}
