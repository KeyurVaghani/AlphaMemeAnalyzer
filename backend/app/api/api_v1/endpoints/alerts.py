from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.memecoin import Memecoin, Alert
from app.services.notifications import send_notification

router = APIRouter()

@router.post("/{memecoin_id}")
def create_alert(
    *,
    db: Session = Depends(get_db),
    memecoin_id: int,
    alert_type: str,
    threshold: float,
    notification_channel: str = "telegram"  # telegram, email, etc.
):
    """
    Create a new alert for a memecoin.
    """
    memecoin = db.query(Memecoin).filter(Memecoin.id == memecoin_id).first()
    if not memecoin:
        raise HTTPException(status_code=404, detail="Memecoin not found")
    
    alert_data = {
        "type": alert_type,
        "threshold": threshold,
        "notification_channel": notification_channel
    }
    
    alert = Alert(
        memecoin_id=memecoin_id,
        alert_type=alert_type,
        alert_data=alert_data,
        is_active=True
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    return {"message": "Alert created successfully", "alert_id": alert.id}

@router.get("/active", response_model=List[dict])
def get_active_alerts(
    *,
    db: Session = Depends(get_db)
):
    """
    Get all active alerts.
    """
    alerts = db.query(
        Alert,
        Memecoin.name,
        Memecoin.symbol
    ).join(
        Memecoin
    ).filter(
        Alert.is_active == True
    ).all()
    
    return [
        {
            "id": alert.Alert.id,
            "memecoin_name": alert.name,
            "memecoin_symbol": alert.symbol,
            "type": alert.Alert.alert_type,
            "data": alert.Alert.alert_data
        }
        for alert in alerts
    ]

@router.post("/{alert_id}/trigger", status_code=200)
async def trigger_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int,
    background_tasks: BackgroundTasks,
    trigger_data: dict
):
    """
    Trigger an alert and send notifications.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    memecoin = db.query(Memecoin).filter(Memecoin.id == alert.memecoin_id).first()
    
    notification_data = {
        "memecoin_name": memecoin.name,
        "memecoin_symbol": memecoin.symbol,
        "alert_type": alert.alert_type,
        "trigger_data": trigger_data
    }
    
    # Queue notification in background
    background_tasks.add_task(
        send_notification,
        alert.alert_data["notification_channel"],
        notification_data
    )
    
    return {"message": "Alert triggered successfully"}

@router.delete("/{alert_id}")
def delete_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int
):
    """
    Delete an alert.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    db.delete(alert)
    db.commit()
    
    return {"message": "Alert deleted successfully"}

@router.put("/{alert_id}/deactivate")
def deactivate_alert(
    *,
    db: Session = Depends(get_db),
    alert_id: int
):
    """
    Deactivate an alert without deleting it.
    """
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_active = False
    db.add(alert)
    db.commit()
    
    return {"message": "Alert deactivated successfully"} 