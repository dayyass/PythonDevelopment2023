import asyncio
import shlex
from cowsay import list_cows, cowsay


clients = {}
login_clients = {}

async def chat(reader, writer):

    me = "{}:{}".format(*writer.get_extra_info('peername'))
    print(me)

    clients[me] = asyncio.Queue()

    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())

    login = False

    while not reader.at_eof():
        done, _ = await asyncio.wait(
            [send, receive],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for q in done:
            if q is send:

                send = asyncio.create_task(reader.readline())
                parsed_cmd = shlex.split(q.result().decode().strip())
                cmd, parsed_args = parsed_cmd[0], parsed_cmd[1:]

                if cmd == "exit":
                    break

                elif cmd == "login":
                    cow_name = parsed_args[0]
                    if cow_name in list_cows():
                        if cow_name not in login_clients.values():
                            login_clients[me] = cow_name
                            login = True
                            await clients[me].put(f"Success login {me} as {cow_name}")
                        else:
                            await clients[me].put(f"Login {cow_name} already in use")
                    else:
                        await clients[me].put(f"Unknown cow name {cow_name}")
                
                elif cmd == "who":
                    if len(login_clients.values()) == 0:
                        res = "No one authorized"
                    else:
                        res = '\n'.join(login_clients.values())
                    await clients[me].put(res)

                elif cmd == "cows":
                    await clients[me].put('\n'.join(sorted(set(list_cows()) - set(login_clients.values()))))
                
                elif login:
                    if cmd == "say":
                        for ip, cow in login_clients.items():
                            if cow == parsed_args[0]:
                                await clients[ip].put(cowsay(parsed_args[1], cow=login_clients[me]))

                    elif cmd == "yield":
                        for client in clients.values():
                            await client.put(cowsay(parsed_args[0], cow=login_clients[me]))

                else:
                    await clients[me].put(f"You are not authorized")  

                for out in clients.values():
                    if out is not clients[me]:
                        await out.put(f"{me} {q.result().decode().strip()}")
            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()

    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    del login_clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
