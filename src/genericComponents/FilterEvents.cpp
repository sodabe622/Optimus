/******************************************************************************
*                 SOFA, Simulation Open-Framework Architecture                *
*                    (c) 2006 INRIA, USTL, UJF, CNRS, MGH                     *
*                                                                             *
* This program is free software; you can redistribute it and/or modify it     *
* under the terms of the GNU General Public License as published by the Free  *
* Software Foundation; either version 2 of the License, or (at your option)   *
* any later version.                                                          *
*                                                                             *
* This program is distributed in the hope that it will be useful, but WITHOUT *
* ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       *
* FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    *
* more details.                                                               *
*                                                                             *
* You should have received a copy of the GNU General Public License along     *
* with this program. If not, see <http://www.gnu.org/licenses/>.              *
*******************************************************************************
* Authors: The SOFA Team and external contributors (see Authors.txt)          *
*                                                                             *
* Contact information: contact@sofa-framework.org                             *
******************************************************************************/


#include <sofa/core/objectmodel/Event.h>
#include "initOptimusPlugin.h"
#include "FilterEvents.h"


namespace sofa
{

namespace component
{

namespace stochastic
{


SOFA_EVENT_CPP( PredictionEndEvent )

PredictionEndEvent::PredictionEndEvent(SReal dt)
    : sofa::core::objectmodel::Event()
    , dt(dt)
{
}


PredictionEndEvent::~PredictionEndEvent()
{
}

SOFA_EVENT_CPP( CorrectionEndEvent )

CorrectionEndEvent::CorrectionEndEvent(SReal dt)
    : sofa::core::objectmodel::Event()
    , dt(dt)
{
}


CorrectionEndEvent::~CorrectionEndEvent()
{
}



}  /// sofa

}  /// component

}  /// stochastic

