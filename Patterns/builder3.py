class SelectQueryBuilder:
    def __init__(self):
        self._select_columns = []
        self._from_table = ""
        self._joins = []
        self._where_conditions = []
        self._order_by_column = ""
        self._order_by_direction = ""
        self._limit_value = None
        self._offset_value = None

    def select(self, *columns):
        self._select_columns = list(columns)
        return self

    def from_table(self, table: str):
        self._from_table = table
        return self

    def join(self, table: str, condition: str):
        self._joins.append((table, condition))
        return self

    def where(self, condition: str):
        self._where_conditions.append(condition)
        return self

    def order_by(self, column: str, direction: str = "ASC"):
        self._order_by_column = column
        self._order_by_direction = direction
        return self

    def limit(self, value: int):
        self._limit_value = value
        return self

    def offset(self, value: int):
        self._offset_value = value
        return self

    def build(self) -> str:
        parts = []

        if self._select_columns:
            select_clause = f"SELECT {', '.join(self._select_columns)}"
        else:
            select_clause = "SELECT *"
        parts.append(select_clause)

        if not self._from_table:
            raise ValueError("FROM table is required")
        parts.append(f"FROM {self._from_table}")

        for table, condition in self._joins:
            parts.append(f"JOIN {table} ON {condition}")

        if self._where_conditions:
            where_clause = f"WHERE {' AND '.join(self._where_conditions)}"
            parts.append(where_clause)

        if self._order_by_column:
            parts.append(f"ORDER BY {self._order_by_column} {self._order_by_direction}")

        if self._limit_value is not None:
            parts.append(f"LIMIT {self._limit_value}")

        if self._offset_value is not None:
            parts.append(f"OFFSET {self._offset_value}")

        return "\n".join(parts)