from typing import List, Dict, Optional
from model.estudante import *


class estudanteService:
    def __init__(self):
        self.estudante: Dict[str, estudante] = {}

    def criarEstudante(self, student_data: criarestudante) -> estudante:
        student = estudante(**student_data.dict())
        self.estudante[student.id] = student
        return student

    def getTodos(self) -> List[estudante]:
        return list(self.estudante.values())

    def getestudanteId(self, estudante_id: str) -> Optional[estudante]:
        return self.estudante.get(estudante_id)

    def updateEstudante(self, estudante_id: str, student_data: estudanteUpdate) -> Optional[estudante]:
        if estudante_id not in self.estudante:
            return None

        updated_student = estudante(id=estudante_id, **student_data.dict())
        self.estudante[estudante_id] = updated_student
        return updated_student

    def delete_student(self, estudante_id: str) -> bool:
        if estudante_id in self.estudante:
            del self.estudante[estudante_id]
            return True
        return False

    def calculate_student_average(self, student: estudante) -> float:
        return sum(student.grades) / len(student.grades)

    def calculate_class_average_per_subject(self) -> List[float]:
        if not self.estudante:
            return [0.0] * 5

        estudante_list = list(self.estudante.values())
        subject_averages = []

        for subject_index in range(5):
            subject_sum = sum(student.grades[subject_index] for student in estudante_list)
            subject_avg = subject_sum / len(estudante_list)
            subject_averages.append(round(subject_avg, 2))

        return subject_averages

    def calculate_class_average(self) -> float:
        if not self.estudante:
            return 0.0

        total_average = sum(
            self.calculate_student_average(student)
            for student in self.estudante.values()
        )
        return round(total_average / len(self.estudante), 2)

    def get_estudante_above_average(self) -> List[Dict]:
        class_avg = self.calculate_class_average()

        estudante_above = []
        for student in self.estudante.values():
            student_avg = self.calculate_student_average(student)
            if student_avg > class_avg:
                estudante_above.append({
                    "id": student.id,
                    "name": student.name,
                    "average": round(student_avg, 2)
                })

        return estudante_above

    def get_estudante_below_attendance_threshold(self, threshold: float = 75.0) -> List[Dict]:
        estudante_below = []

        for student in self.estudante.values():
            if student.attendance < threshold:
                estudante_below.append({
                    "id": student.id,
                    "name": student.name,
                    "attendance": student.attendance
                })

        return estudante_below

    def get_report(self) -> Dict:
        estudante_list = self.getTodos()

        estudante_with_averages = [
            {
                "id": student.id,
                "name": student.name,
                "grades": student.grades,
                "attendance": student.attendance,
                "average": round(self.calculate_student_average(student), 2)
            }
            for student in estudante_list
        ]

        return {
            "total_estudante": len(estudante_list),
            "estudante": estudante_with_averages,
            "class_average": self.calculate_class_average(),
            "class_average_per_subject": self.calculate_class_average_per_subject(),
            "estudante_above_average": self.get_estudante_above_average(),
            "estudante_below_attendance": self.get_estudante_below_attendance_threshold()
        }


student_service = estudanteService()
