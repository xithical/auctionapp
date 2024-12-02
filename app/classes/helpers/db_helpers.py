from playhouse.shortcuts import model_to_dict

class DatabaseHelpers:
    @staticmethod
    def get_rows(query):
        rows = []

        try:
            if query.count() > 0:
                for object in query:
                    rows.append(model_to_dict(object))
        except Exception as e:
            print(f"{__name__} - Database Error: {e}")
        
        return rows