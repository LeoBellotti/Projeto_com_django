# Generated by Django 5.1.1 on 2024-11-24 16:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ConteudoLogin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_login', models.CharField(max_length=50)),
                ('titulo', models.CharField(max_length=100)),
                ('imagem_fundo', models.ImageField(blank=True, null=True, upload_to='imagens/')),
            ],
        ),
        migrations.CreateModel(
            name='PaginaInicial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(default='Bem-vindo à Cervejaria', max_length=200)),
                ('imagem_fundo', models.ImageField(blank=True, null=True, upload_to='imagens/')),
                ('link_login_gerente', models.CharField(default='/login/gerente/', max_length=200)),
                ('link_login_produtor', models.CharField(default='/login/produtor/', max_length=200)),
                ('atualizado_em', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Produtor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=150, unique=True)),
                ('senha', models.CharField(max_length=255)),
                ('nome', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('telefone', models.CharField(max_length=15)),
                ('cpf', models.CharField(blank=True, max_length=15, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'produtor',
            },
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('tipo', models.CharField(choices=[('malte', 'Malte'), ('lupulo', 'Lúpulo'), ('levedura', 'Levedura'), ('agua', 'Água'), ('produto_final', 'Produto Final')], max_length=20)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantidade', models.IntegerField(default=0)),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'unique_together': {('nome', 'tipo')},
            },
        ),
        migrations.CreateModel(
            name='Estoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField(default=0)),
                ('valor_total', models.DecimalField(decimal_places=2, max_digits=15)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('data_criacao', models.DateTimeField(auto_now_add=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
                ('produtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pedidos', to='produtos.produtor')),
            ],
        ),
        migrations.CreateModel(
            name='LogSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('acao', models.CharField(max_length=255)),
                ('data_entrada', models.DateTimeField(auto_now_add=True)),
                ('produtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produtor')),
            ],
            options={
                'db_table': 'LogSistema',
            },
        ),
        migrations.CreateModel(
            name='EstoqueChange',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('tipo_alteracao', models.CharField(max_length=50)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
                ('produtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produtor')),
            ],
        ),
        migrations.CreateModel(
            name='RelatorioEstoque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade_alterada', models.IntegerField()),
                ('tipo_alteracao', models.CharField(max_length=50)),
                ('data', models.DateTimeField(auto_now_add=True)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produto')),
                ('produtor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produtos.produtor')),
            ],
            options={
                'db_table': 'RelatorioEstoque',
            },
        ),
    ]
