from orator.migrations import Migration


class AddDataColumn(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('secrets') as table:
            table.text('data').default('')

    def down(self):
        """
        Revert the migrations.
        """
        with self.schema.table('secrets') as table:
            table.drop_column('data')
