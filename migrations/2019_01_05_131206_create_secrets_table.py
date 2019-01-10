from orator.migrations import Migration


class CreateSecretsTable(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.db.transaction():
            with self.schema.create('secrets') as table:
                table.increments('id')
                table.string('url')
                table.text('credentials')
                table.json('tags')
                table.integer('category_id').unsigned()
                table.foreign('category_id').references('id').on('categories')
                table.timestamps()

    def down(self):
        """
        Revert the migrations.
        """
        with self.db.transaction():
            self.schema.drop('secrets')
