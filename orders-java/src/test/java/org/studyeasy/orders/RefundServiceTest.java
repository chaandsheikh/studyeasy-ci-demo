package org.studyeasy.orders;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

class RefundServiceTest {

    private final RefundService refunds = new RefundService();
    private final BigDecimal orderTotal = new BigDecimal("40.00");

    @Test
    void halfRefund() {
        assertEquals(new BigDecimal("20.00"), refunds.refundAmount(orderTotal, 50));
    }

    @Test
    void fullRefundIsTheOrderTotal() {
        assertEquals(orderTotal, refunds.refundAmount(orderTotal, 100));
    }

    @Test
    void percentOutOfRangeIsRejected() {
        assertThrows(IllegalArgumentException.class, () -> refunds.refundAmount(orderTotal, 101));
        assertThrows(IllegalArgumentException.class, () -> refunds.refundAmount(orderTotal, -1));
    }
}
