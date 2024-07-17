// elastic_buffer.sv

`default_nettype none

module elastic_buffer # (
  parameter int DLEN    = 8 // Data Width
)(
  input var                     clk,
  input var                     rstn,

  input var                     i_valid,
  output var logic              o_ready,
  input var         [DLEN-1:0]  i_data,

  output var logic              o_valid,
  input var                     i_ready,
  output var logic  [DLEN-1:0]  o_data
);

logic valid_buf;
always_ff @(posedge clk) begin
  if (!rstn) begin
    valid_buf <= 0;
  end else begin
    if (valid_buf) begin
      valid_buf <= !i_ready;
    end else begin
      valid_buf <= i_valid & o_valid & ~i_ready;
    end
  end
end

always_ff @(posedge clk) begin
  if (!rstn) begin
    o_valid <= 0;
  end else begin
    if (o_valid) begin
      o_valid <= i_valid | valid_buf;
    end else begin
      o_valid <= i_valid;
    end
  end
end

logic [DLEN-1:0] data_buf;
always_ff @(posedge clk) begin
  if (o_valid && !valid_buf && !i_ready) begin
    data_buf <= i_data;
  end else begin
    data_buf <= data_buf;
  end
end

always_ff @(posedge clk) begin
  if (valid_buf && i_ready) begin
    o_data <= data_buf;
  end else if ((i_valid && !o_valid) || (i_valid && i_ready)) begin
    o_data <= i_data;
  end else begin
    o_data <= o_data;
  end
end

always_ff @(posedge clk) begin
  if (!rstn) begin
    o_ready <= 0;
  end else begin
    o_ready <= ~(i_valid & o_valid) | i_ready;
  end
end

endmodule
