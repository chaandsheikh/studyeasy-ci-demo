package org.studyeasy.orders;

import java.math.BigDecimal;
import java.math.RoundingMode;

/** Order totals for the orders service. */
public class OrderService {

    public BigDecimal total(BigDecimal unitPrice, int quantity) {
        if (quantity < 1) {
            throw new IllegalArgumentException("quantity must be at least 1");
        }
        return unitPrice.multiply(BigDecimal.valueOf(quantity)).setScale(2, RoundingMode.HALF_UP);
    }
}
