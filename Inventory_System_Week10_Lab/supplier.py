
class Supplier:
    def __init__(self,supplier_id : str,name : str ,contact_email : str) -> None:
        self._supplier_id: str = supplier_id
        self._name: str= name
        self._contact_email: str = contact_email

    def display_information(self)->None:
        print(f"Supplier id: {self._supplier_id} | "
            f"Name: {self._name}"
            f"Contact email: {self._contact_email}")