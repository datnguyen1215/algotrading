How does it perform 70% guess rate?

## Labels
Since we cannot determine how strong the candles are, we need to calculate the next candle's direction based on the previous candles.

However, instead of using only diff(), we should use the angles.

## Data
Using angles are better than raw values because it shows the actual direction of the move.