package org.studyeasy.orders;

import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.logging.Logger;

/** Refunds for orders. */
public class RefundService {

    private static final Logger LOG = Logger.getLogger(RefundService.class.getName());

    /** A partial refund of an order, in the order's currency. */
    public BigDecimal refundAmount(BigDecimal orderTotal, int percent) {
        if (percent < 0 || percent > 100) {
            throw new IllegalArgumentException("percent must be between 0 and 100");
        }
        return orderTotal.multiply(BigDecimal.valueOf(percent))
                .divide(BigDecimal.valueOf(100), 2, RoundingMode.HALF_UP);
    }

    /** A partial refund plus a goodwill bonus for a late order. */
    public BigDecimal goodwillRefund(BigDecimal orderTotal, int percent, BigDecimal bonus, Customer customer) {
        BigDecimal amount = refundAmount(orderTotal, percent).add(bonus).min(orderTotal);
        LOG.info("goodwill refund " + amount + " to " + customer.id());
        return amount;
    }
}
