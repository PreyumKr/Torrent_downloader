#!/usr/bin/env python
"""Check aria2c status and control downloads (pause / remove).

Usage examples:
  python check_aria2.py --list
  python check_aria2.py --pause <GID>
  python check_aria2.py --remove <GID>
  python check_aria2.py          # interactive menu
"""
import argparse
import asyncio
import websockets
import json
from typing import List, Dict, Any, Optional

ARIA2_RPC = "ws://localhost:6800/jsonrpc"


async def rpc_call(method: str, params: List = None) -> Dict[str, Any]:
    params = params or []
    async with websockets.connect(ARIA2_RPC) as ws:
        msg = {"jsonrpc": "2.0", "id": "cli", "method": method, "params": params}
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        return json.loads(resp)


async def list_active() -> List[Dict[str, Any]]:
    res = await rpc_call("aria2.tellActive", [])
    return res.get("result", [])


def format_entry(i: int, d: Dict[str, Any]) -> str:
    gid = d.get("gid")
    name = d.get("files", [{}])[0].get("path", "Unknown").split('/')[-1]
    completed = int(d.get("completedLength", 0))
    total = int(d.get("totalLength", 1))
    try:
        progress = completed / total * 100 if total > 0 else 0.0
    except Exception:
        progress = 0.0
    status = d.get("status", "unknown")
    return f"{i}. GID: {gid} | {name} | {status} | {progress:.1f}%"


async def do_pause(gid: str) -> Dict[str, Any]:
    return await rpc_call("aria2.pause", [gid])


async def do_remove(gid: str) -> Dict[str, Any]:
    return await rpc_call("aria2.remove", [gid])


async def do_force_remove(gid: str) -> Dict[str, Any]:
    return await rpc_call("aria2.forceRemove", [gid])


async def interactive_menu():
    actives = await list_active()
    if not actives:
        print("No active downloads.")
        return

    print("Active downloads:")
    for i, d in enumerate(actives, 1):
        print(format_entry(i, d))

    try:
        choice = input("\nEnter number to control, or 'q' to quit: ").strip()
    except (EOFError, KeyboardInterrupt):
        return

    if choice.lower() == 'q' or not choice:
        return

    try:
        idx = int(choice) - 1
        if idx < 0 or idx >= len(actives):
            print("Invalid selection")
            return
    except ValueError:
        print("Please enter a number")
        return

    gid = actives[idx].get('gid')
    print(f"Selected GID: {gid}")
    print("Actions: 1) pause  2) remove  3) force-remove  4) cancel")
    action = input("Choose action (1-4): ").strip()
    if action == '1':
        r = await do_pause(gid)
        print(f"Pause result: {r}")
    elif action == '2':
        r = await do_remove(gid)
        print(f"Remove result: {r}")
    elif action == '3':
        r = await do_force_remove(gid)
        print(f"Force remove result: {r}")
    else:
        print("Canceled")


def main():
    # Terminal-style interactive loop (numbered menu)
    try:
        while True:
            print('\n=== aria2 Interactive Menu ===')
            print('1) List active downloads')
            print('2) Pause a download (by index)')
            print('3) Remove a download (by index)')
            print('4) Force-remove a download (by index)')
            print('5) Refresh / Show active downloads')
            print('6) Quit')

            choice = input('\nSelect option (1-6): ').strip()
            if choice == '1' or choice == '5':
                actives = asyncio.run(list_active())
                if not actives:
                    print('\nNo active downloads')
                    continue
                print('\nActive downloads:')
                for i, d in enumerate(actives, 1):
                    print(format_entry(i, d))

            elif choice in ('2', '3', '4'):
                actives = asyncio.run(list_active())
                if not actives:
                    print('\nNo active downloads')
                    continue
                print('\nActive downloads:')
                for i, d in enumerate(actives, 1):
                    print(format_entry(i, d))

                idx_input = input('\nEnter download number to act on (or q to cancel): ').strip()
                if idx_input.lower() == 'q' or not idx_input:
                    continue
                try:
                    idx = int(idx_input) - 1
                except ValueError:
                    print('Invalid number')
                    continue
                if idx < 0 or idx >= len(actives):
                    print('Selection out of range')
                    continue
                gid = actives[idx].get('gid')
                if choice == '2':
                    print('Pausing...')
                    res = asyncio.run(do_pause(gid))
                    print(res)
                elif choice == '3':
                    print('Removing...')
                    res = asyncio.run(do_remove(gid))
                    print(res)
                else:
                    print('Force removing...')
                    res = asyncio.run(do_force_remove(gid))
                    print(res)

            elif choice == '6':
                print('\nExiting...')
                break
            else:
                print('Invalid selection, choose 1-6')
    except (KeyboardInterrupt, EOFError):
        print('\nExiting...')
    except Exception as e:
        print(f'Error in interactive loop: {e}')


if __name__ == '__main__':
    main()
