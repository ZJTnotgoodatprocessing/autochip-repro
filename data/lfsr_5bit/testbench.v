`timescale 1ns / 1ps

module testbench;
    reg clk, reset;
    wire [4:0] q;
    wire [4:0] expected_q;

    top_module dut(.clk(clk), .reset(reset), .q(q));

    // Golden model
    reg [4:0] golden_q;
    always @(posedge clk) begin
        if (reset)
            golden_q <= 5'b00001;
        else
            golden_q <= {golden_q[3:0], golden_q[4] ^ golden_q[2]};
    end
    assign expected_q = golden_q;

    integer total_samples = 0;
    integer mismatches = 0;

    task check;
        begin
            total_samples = total_samples + 1;
            if (q !== expected_q) begin
                mismatches = mismatches + 1;
                $display("MISMATCH at time %0t: q=%b expected=%b",
                         $time, q, expected_q);
            end
        end
    endtask

    // Clock generation
    initial clk = 0;
    always #5 clk = ~clk;

    integer i;
    initial begin
        // Reset
        reset = 1;
        @(posedge clk); #1;
        @(posedge clk); #1;
        reset = 0;

        // Check first state after reset
        @(posedge clk); #1; check;

        // Run for 35 cycles to cover the full LFSR period and beyond
        for (i = 0; i < 35; i = i + 1) begin
            @(posedge clk); #1; check;
        end

        // Test reset in the middle
        reset = 1;
        @(posedge clk); #1;
        @(posedge clk); #1;
        reset = 0;

        // Run another 10 cycles after re-reset
        for (i = 0; i < 10; i = i + 1) begin
            @(posedge clk); #1; check;
        end

        $display("Hint: Total mismatched samples is %0d out of %0d samples", mismatches, total_samples);
        if (mismatches == 0) $display("ALL TESTS PASSED");
        else $display("SOME TESTS FAILED");
        $finish;
    end
endmodule
