class User:

    def __init__(self, personal_id: int, ssn: int, name: str, is_member: bool):
        self.id = personal_id
        self.ssn = ssn
        self.name = name
        self.is_member = is_member

    def GetFormattedUser(self) -> dict:
         return {str(self.id): {"ssn": self.ssn, "name": self.name, "is_member": self.is_member}}
