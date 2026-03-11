from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('armodels', '0002_alter_armodel_glb_file_alter_armodel_usdz_file'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='armodel',
            name='owner',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='models',
                to='authentication.user',
            ),
        ),
    ]
