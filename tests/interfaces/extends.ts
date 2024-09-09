interface Person {
  id: number;
  name: string;
  age: number;
}

interface Employee extends Person {
  employeeId: number;
  department: string;
}

interface Manager extends Employee {
  teamSize: number;
  managesDepartments: string[];
}

interface Supervisor extends Person, Manager {
  supervisorId: number;
}

interface Response<T> extends Employee {
  data: T;
  status: string;
}
