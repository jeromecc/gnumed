<?php
// PHP interface to gnumed drug database
// Copyright (C) 2002 Ian Haywood 

// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
// or see online at http://www.gnu.org/licenses/gpl.html

# page to receive a new component of a compound drug
include ('connect.php');
$result = pg_query ("select id_drug from generic_drug_name where name = '$drug'");

if (pg_num_rows ($result) != 1)
{
  echo "Aargh! no drug $drug. Go back!";
}
else
{
  $otherdrugid = pg_fetch_result ($result, 0, 0);
  pg_query ("insert into link_compound_generics values ($id, $otherdrugid)");
  $message = "new compound component added";
  include ('viewcompound.php');
}
?>