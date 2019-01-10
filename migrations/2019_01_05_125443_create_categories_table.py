from orator.migrations import Migration


class CreateCategoriesTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.db.transaction():
            with self.schema.create('categories') as table:
                table.increments('id')
                table.string('name')
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        with self.db.transaction():
            self.schema.drop('categories')
