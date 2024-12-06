
.PHONY: app
app:
	make -C ./DataBase app
	make -C ./AuthService app
	make -C ./UserService app
	make -C ./GateWay app

.PHONY: app-up
app-up:
	make -C ./DataBase app-up
	make -C ./AuthService app-up
	make -C ./UserService app-up
	make -C ./GateWay app-up

.PHONY: app-down
app-down:
	make -C ./DataBase app-down
	make -C ./AuthService app-down
	make -C ./UserService app-down
	make -C ./GateWay app-down


.PHONY: auth-shell
auth-shell:
	make -C ./AuthService app-shell

.PHONY: pg-shell
pg-shell:
	make -C ./DataBase app-shell

.PHONY: gateway-shell
gateway-shell:
	make -C ./GateWay app-shell

.PHONY: user-shell
user-shell:
	make -C ./UserService app-shell


.PHONY: auth-logs
auth-logs:
	make -C ./AuthService app-logs

.PHONY: pg-logs
pg-logs:
	make -C ./DataBase app-logs

.PHONY: gateway-logs
gateway-logs:
	make -C ./GateWay app-logs

.PHONY: user-logs
user-logs:
	make -C ./UserService app-logs