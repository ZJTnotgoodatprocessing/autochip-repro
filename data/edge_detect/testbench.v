`timescale 1ns / 1ps

module testbench;
    reg clk, reset, in;
    wire rise;
    wire expected_rise;

    top_module dut(.clk(clk), .reset(reset), .in(in), .rise(rise));

    // Golden model: detect 0->1 transition
    reg prev_in;
    always @(posedge clk) begin
        if (reset)
            prev_in <= 0;
        else
            prev_in <= in;
    end
    assign expected_rise = (~prev_in & in) & ~reset;

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (rise !== expected_rise) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: in=%b prev_in=%b rise=%b expected=%b",
                         $time, in, prev_in, rise, expected_rise);
            end
        end
    endtask

    // Clock generation
    initial clk = 0;
    always #5 clk = ~clk;

    initial begin
        // Reset sequence
        reset = 1; in = 0;
        @(posedge clk); #1;
        @(posedge clk); #1;
        reset = 0;

        // Test: stay low
        in = 0; @(posedge clk); #1; check;

        // Test: rising edge -> should detect
        in = 1; @(posedge clk); #1; check;

        // Test: stay high -> no edge
        in = 1; @(posedge clk); #1; check;

        // Test: falling edge -> no detect
        in = 0; @(posedge clk); #1; check;

        // Test: another rising edge
        in = 1; @(posedge clk); #1; check;

        // Test: drop and rise again
        in = 0; @(posedge clk); #1; check;
        in = 1; @(posedge clk); #1; check;

        // Test: multiple cycles high
        in = 1; @(posedge clk); #1; check;
        in = 1; @(posedge clk); #1; check;

        // Test: reset while high
        reset = 1; in = 1; @(posedge clk); #1; check;
        reset = 0; in = 1; @(posedge clk); #1; check;

        // Test: rise immediately after reset release
        in = 0; @(posedge clk); #1; check;
        in = 1; @(posedge clk); #1; check;

        // Test: rapid toggling
        in = 0; @(posedge clk); #1; check;
        in = 1; @(posedge clk); #1; check;
        in = 0; @(posedge clk); #1; check;
        in = 1; @(posedge clk); #1; check;
        in = 0; @(posedge clk); #1; check;

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
