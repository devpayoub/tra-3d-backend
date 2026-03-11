from django.db import migrations, models
import armodels.models


class Migration(migrations.Migration):

    dependencies = [
        ('armodels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='armodel',
            name='glb_file',
            field=models.FileField(blank=True, null=True, upload_to=armodels.models.model_upload_path),
        ),
        migrations.AlterField(
            model_name='armodel',
            name='usdz_file',
            field=models.FileField(blank=True, null=True, upload_to=armodels.models.model_upload_path),
        ),
    ]
