// g2o - General Graph Optimization
// Copyright (C) 2011 R. Kuemmerle, G. Grisetti, W. Burgard
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
// * Redistributions of source code must retain the above copyright notice,
//   this list of conditions and the following disclaimer.
// * Redistributions in binary form must reproduce the above copyright
//   notice, this list of conditions and the following disclaimer in the
//   documentation and/or other materials provided with the distribution.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
// IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
// TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
// PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
// TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
// PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
// LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
// NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
// SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#include "g2o/config.h"
#include "g2o/core/factory.h"
#include "types_sclam2d.h"
#include "g2o/stuff/macros.h"

namespace g2o {

    G2O_USE_TYPE_GROUP(slam2d);

    G2O_REGISTER_TYPE_GROUP(sclam);
    G2O_REGISTER_TYPE(VERTEX_ODOM_DIFFERENTIAL, VertexOdomDifferentialParams);
    G2O_REGISTER_TYPE(EDGE_SE2_CALIB, EdgeSE2SensorCalib);
    G2O_REGISTER_TYPE(EDGE_SE2_ODOM_DIFFERENTIAL_CALIB, EdgeSE2OdomDifferentialCalib);

    G2O_REGISTER_TYPE(NODE_SE2, NodeSE2)
//    G2O_REGISTER_TYPE(NODE_V1, NodeV1)
    G2O_REGISTER_TYPE(NODE_V2, NodeV2)
//    G2O_REGISTER_TYPE(NODE_V3, NodeV3)
    G2O_REGISTER_TYPE(PARAMETER_SE2, ParameterSE2)
    G2O_REGISTER_TYPE(PARAMETER_V1, ParameterV1)
    G2O_REGISTER_TYPE(PARAMETER_V2, ParameterV2)
    G2O_REGISTER_TYPE(PARAMETER_V3, ParameterV3)

    G2O_REGISTER_TYPE(CONSTRAINT_POSE2D_V2, ConstraintPose2DV2)
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2, ConstraintPoses2DSE2)
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_SE2, ConstraintPoses2DSE2SE2)
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_V1, ConstraintPoses2DSE2V1)
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_V2, ConstraintPoses2DSE2V2)
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_V3, ConstraintPoses2DSE2V3)


    G2O_REGISTER_TYPE(INFO3, Info3)
    G2O_REGISTER_TYPE(CONSTRAINT_INFO3, ConstraintInfo3)
    G2O_REGISTER_TYPE(CONSTRAINT_POSES2D_SE2_I3, ConstraintPoses2DSE2I)

#ifdef G2O_HAVE_OPENGL
  G2O_REGISTER_ACTION(EdgeSE2SensorCalibDrawAction);
  G2O_REGISTER_ACTION(EdgeSE2OdomDifferentialCalibDrawAction);
#endif

} // end namespace
