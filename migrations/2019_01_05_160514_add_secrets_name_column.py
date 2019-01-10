from orator.migrations import Migration


class AddSecretsNameColumn(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.db.transaction():
            with self.schema.table('secrets') as table:
                table.string('name')

    def down(self):
        """
        Revert the migrations.
        """
        pass
