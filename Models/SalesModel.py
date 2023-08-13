from Models.GeneralModel import GeneralModel
from Models.ProductsModel import ProductsModel

Q={
    "register_sale":"INSERT INTO sales(code,lot,sale_price,date) VALUES (?,?,?,CURRENT_DATE())",
    "verify_product":"SELECT * FROM sales WHERE code=? AND date=CURRENT_DATE()",
    "update_sale":"UPDATE sales SET lot=lot+?,sale_price=sale_price+? WHERE code=? AND date=CURRENT_DATE()",
}

class SalesModel(GeneralModel):

    def __init__(self):
        self.__ProductsModel=ProductsModel()

    def register_sale(self, code:str, lot:int):
        product=self.__ProductsModel.read_product(code)
        if product!=[]:
            if self.run_get_query(Q.get("verify_product"),(code,))==[]:
                #Insertar Venta del Producto en el día
                resp=self.run_set_query(Q.get("register_sale"),(code,lot,product[0][4]))
                if type(resp)==int:
                    status="Success" if (resp>0) else "No se insertó"
                else:
                    status=resp
            else:
                #Actualizar Venta del Producto en el día
                resp=self.run_set_query(Q.get("update_sale"),(lot,product[0][4],code))
                if type(resp)==int:
                    status="Success" if (resp>0) else "No se actualizó"
                else:
                    status=resp
        else:
            status="No existe ese producto"
        return status

