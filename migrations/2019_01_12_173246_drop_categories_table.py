from orator.migrations import Migration


class DropCategoriesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('categories') as table:
            table.drop()

    def down(self):
        """
        Revert the migrations.
        """
        pass
