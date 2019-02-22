from orator.migrations import Migration


class DeleteUnsusedColumns(Migration):

    def up(self):
        """
        Run the migrations.
        """
        with self.schema.table('secrets') as table:
            table.drop_column('name')
            table.drop_column('category_id')
            table.drop_column('tags')
            table.drop_column('credentials')
            table.drop_column('url')

    def down(self):
        """
        Revert the migrations.
        """
        pass
