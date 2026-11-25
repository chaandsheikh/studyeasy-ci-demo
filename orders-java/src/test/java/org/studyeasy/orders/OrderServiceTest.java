package org.studyeasy.orders;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import org.junit.jupiter.api.Test;

class OrderServiceTest {

    private final OrderService orders = new OrderService();

    @Test
    void totalIsPriceTimesQuantity() {
        assertEquals(new BigDecimal("39.99"), orders.total(new BigDecimal("13.33"), 3));
    }

    @Test
    void quantityMustBePositive() {
        assertThrows(IllegalArgumentException.class, () -> orders.total(new BigDecimal("10.00"), 0));
    }
}
