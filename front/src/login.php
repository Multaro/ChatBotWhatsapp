<!DOCTYPE html>
<html lang="pt-br">

<head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-gH2yIJqKdNHPEq0n4Mqa/HGKIhSkIHeL5AyhkYV8i59U5AR6csBvApHHNl/vI1Bx" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-A3rJD856KowSb7dwlZdYEkO39Gagi7vIsF0jrRAoQmDKKtQBHUuLZ9AsSv4jD4Xa" crossorigin="anonymous"></script>
  <link href='http://fonts.googleapis.com/css?family=Roboto:400,100,100italic,300,300italic,400italic,500,500italic,700,700italic,900italic,900' rel='stylesheet' type='text/css'>
  <link rel="stylesheet" type="text/css" href="estilos.css">
  <script src="../js/funcao.js"></script>
  <title>MANAGER</title>
  <meta charset="utf-8">
</head>

<body>
  <div class="container">
    <div class="box_login">
      <div class="alinha_box">
        <!--<div id='login_geral' name='login_geral'>-->
        <div id="titulo_pag">  
          <label style="color: rgb(220, 205, 253);font-family:roboto;font-size:32px;font-weight:bold;margin: top 20px;">MANAGER</label><BR>
          <label style="color: rgb(220, 205, 253);font-family:roboto;font-size:32px;font-weight:bold;margin: top 20px;">LOGIN</label>
        </div>
        <div class="label-float">
          <input type="text" id='user' name='user' placeholder=" " />
          <label style="color: rgb(1, 6,28);">Usuário</label>
        </div>
        <div class="label-float">
          <input id="senha" type="password" placeholder=" " required />
          <label style="color: rgb(1, 6,28);margin-top: -46px;">Senha</label>
        
        </div>
        <div class="label-float">
          <a id="esq_senha"href='dadasds' style="">ESQUECI MINHA SENHA</a>
        </div>
        <div class="label-float">
          <a href="cadastro.php"id="cadastra"href='dadasds' style=""onclick="">CADASTRAR-SE</a>
        </div>           
        <div id="finaliza">       
          <button id="tst"type="button" class="btn btn-red color"style="background-color: rgb(220, 205, 253);"onclick="login();">Entrar</button>
        </div> 
      <!--</div>-->
    </div>
  </div>
</body>

</html>