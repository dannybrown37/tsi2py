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
