<!doctype html>
<html lang="en">
    <head>
        <!-- Required meta tags -->
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
        <!-- Optional JavaScript -->
        <!-- jQuery first, then Popper.js, then Bootstrap JS -->
        <script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>
        <script src="https://kit.fontawesome.com/8cf48e6321.js" crossorigin="anonymous"></script>
        <title>GithLand</title>
    </head>
    <body class="">
        <style>
            header {
                box-shadow: #efefef 1px 1px 1px 1px;
            }
            .info-area {
                background:#efebef;
                font-size:13px;
                border-top: #ccc 1px solid;
                border-bottom: #ccc 1px solid;
            }
            .info-area.ex {
                background:#f9fbe7;
            } 
            .repo {
                box-shadow: #efefef 1px 1px 1px 1px;
            }
            footer {
                background:#efebe9;
                font-size:13px;
            }

        </style>
        <header class="col-sm-12 pt-3 pb-3 text-center">
            <span class="font-weight-bold" style="color:#aaa;">GithLand</span>
        </header>
        <div class="text-center">
            <div class="info-area col-12 p-3 pt-4 pb-4">
                <div class="font-weight-bold" style="font-size:30px;">
                    {{ total_repo }} <span style="font-size:16px;">Repositories</span>
                </div>
                <div class="p-2">
                    <i class="fab fa-3x fa-git-alt" style="color:#ff8a65;"></i>
                </div>
                <p>These datas getting from <a href="https://github.com" target="_blank">github.com</a> by Github API.<br>
                This website source code put on <a href="https://github.com/joichirou/githubResearcher" target="_blank">here</a>.
                </p>
            </div>
        </div>
        <div class="col-12 pt-3 pb-3">
            % top3 = repositories[:3]
            % under = repositories[3:]
            % for repo in top3:
                <div class="repo border rounded mb-3 p-3 pt-4 pb-4 text-center">
                    <a href="{{ repo.owner.url }}" target="_blank"><img class="rounded img-fluid w-50 mb-3" src="{{ repo.owner.avatar_url }}"></a>
                    <div class="font-weight-bold mb-2">
                        <a href="{{repo.url}}" target="_blank">{{ repo.name }}</a>
                    </div>
                    <div>{{ repo.language }} / ⭐️ {{ repo.star }}</div>
                </div>
            % end
        </div>
        <div class="text-center mb-3">
            <div class="info-area ex col-12 p-3 pt-4 pb-4">
                <b>[Search Condition]</b><br>
                <ul class="pl-0 mb-0" style="list-style-type:none;">
                    <li>* Language: Python</li>
                    <li>* Star: 1,000 over</li>
                </ul>
                <div class="p-4 text-info">
                    <i class="fas fa-3x fa-code-branch"></i>
                </div>
                <p>These datas getting from <a href="https://github.com" target="_blank">github.com</a> by Github Api.<br>
                This website source code put on <a href="https://github.com/joichirou/githubResearcher" target="_blank">here</a>.
                </p>
            </div>
        </div>
        <div class="col-12">
            % for repo in under:
                <div class="repo border rounded mb-2 p-2 pt-4 pb-4 row">
                    <div class="" style="width:100px;height:100px;">
                        <a href="{{ repo.owner.url }}" target="_blank"><img class="rounded img-fluid" src="{{ repo.owner.avatar_url }}"></a>
                    </div>
                    <div class="col-7 ml-3 mt-3">
                        <div class="font-weight-bold mb-2">
                            <a href="{{repo.url}}" target="_blank">{{ repo.name }}</a>
                        </div>
                        <div>{{ repo.language }} / ⭐️ {{ repo.star }}</div>
                    </div>
                </div>
            % end
        </div>
        <div class="text-center pt-4 pb-5">
            <a href="#">show more ...</a>
        </div>
    </body>
    <footer class="text-center pt-3 pb-3">
        <a href="https://github.com/joichirou/githubResearcher" target="_blank" style="text-decoration:none;color:#333;"><i class="fab fa-3x fa-github"></i></a>
    </footer>
</html>