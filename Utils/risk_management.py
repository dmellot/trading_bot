def calculate_position_size(capital, risk_percentage, stop_loss_distance):
    """
    Calcule la taille de la position en fonction du capital, du risque maximal et de la distance du stop-loss.
    """
    risk_amount = capital * (risk_percentage / 100)
    position_size = risk_amount / stop_loss_distance
    return position_size

def apply_stop_loss(current_price, stop_loss_percentage):
    """
    Calcule le prix du stop-loss en fonction du prix actuel et du pourcentage de stop-loss.
    """
    stop_loss_price = current_price * (1 - stop_loss_percentage / 100)
    return stop_loss_price