
.PHONY: app
app:
	make -C ./AuthService app
	make -C ./DataBase app

.PHONY: app-up
app-up:
	make -C ./AuthService app-up
	make -C ./DataBase app-up

.PHONY: app-down
app-down:
	make -C ./AuthService app-down
	make -C ./DataBase app-down

.PHONY: auth-shell
auth-shell:
	make -C ./AuthService app-shell

.PHONY: pg-shell
pg-shell:
	make -C ./DataBase app-shell

.PHONY: auth-logs
auth-logs:
	make -C ./AuthService app-logs

.PHONY: pg-logs
pg-logs:
	make -C ./DataBase app-logs
