"""
DrugAI — WebSocket router for real-time progress and metrics.
"""
from __future__ import annotations

import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from celery.result import AsyncResult

from core.logging import get_logger

log = get_logger(__name__)
router = APIRouter(prefix="/ws", tags=["WebSockets"])

@router.websocket("/training/{job_id}")
async def ws_training_progress(websocket: WebSocket, job_id: str):
    await websocket.accept()
    try:
        while True:
            res = AsyncResult(job_id)
            
            if res.state == "PENDING":
                await websocket.send_json({"status": "pending"})
            elif res.state == "TRAINING":
                # 'info' contains the meta dict we passed in update_state
                await websocket.send_json({"status": "training", "meta": res.info})
            elif res.state == "SUCCESS":
                await websocket.send_json({"status": "completed", "result": res.result})
                break
            elif res.state == "FAILURE":
                await websocket.send_json({"status": "failed", "error": str(res.info)})
                break
            else:
                await websocket.send_json({"status": res.state})
                
            await asyncio.sleep(1)
            
    except WebSocketDisconnect:
        log.info("websocket_disconnected", job_id=job_id)

@router.websocket("/notifications")
async def ws_notifications(websocket: WebSocket):
    await websocket.accept()
    try:
        # In production this would subscribe to a Redis PubSub channel
        while True:
            await asyncio.sleep(5)
            await websocket.send_json({"type": "ping", "message": "Heartbeat"})
    except WebSocketDisconnect:
        pass

@router.websocket("/metrics")
async def ws_metrics(websocket: WebSocket):
    await websocket.accept()
    try:
        import psutil
        while True:
            await asyncio.sleep(2)
            cpu = psutil.cpu_percent()
            mem = psutil.virtual_memory().percent
            await websocket.send_json({"cpu_usage": cpu, "memory_usage": mem})
    except WebSocketDisconnect:
        pass
