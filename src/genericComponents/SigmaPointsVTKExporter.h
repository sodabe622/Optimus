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
/*
 * SigmaPointsVTKExporter.h
 */

#pragma once


#include "initOptimusPlugin.h"

#include <sofa/core/objectmodel/BaseObject.h>
#include <sofa/defaulttype/VecTypes.h>
#include <sofa/core/objectmodel/DataFileName.h>
#include <sofa/core/topology/BaseMeshTopology.h>
#include <sofa/core/behavior/BaseMechanicalState.h>
#include <sofa/simulation/Node.h>

#include <fstream>



namespace sofa
{

namespace component
{

namespace misc
{


class SOFA_OPTIMUSPLUGIN_API SigmaPointsVTKExporter : public core::objectmodel::BaseObject
{
public:
    SOFA_CLASS(SigmaPointsVTKExporter,core::objectmodel::BaseObject);

protected:
    sofa::core::topology::BaseMeshTopology* topology;
    sofa::core::behavior::BaseMechanicalState* mstate;
    unsigned int stepCounter;

    std::ofstream* outfile;

    void fetchDataFields(const helper::vector<std::string>& strData, helper::vector<std::string>& objects, helper::vector<std::string>& fields, helper::vector<std::string>& names);
    void writeVTKSimple();
    void writeVTKXML();
    void writeData(const helper::vector<std::string>& objects, const helper::vector<std::string>& fields, const helper::vector<std::string>& names);
    void writeDataArray(const helper::vector<std::string>& objects, const helper::vector<std::string>& fields, const helper::vector<std::string>& names);
    std::string segmentString(std::string str, unsigned int n);

    sofa::simulation::Node* gnode;

public:
    sofa::core::objectmodel::DataFileName vtkFilename;
    Data<bool> fileFormat;	///< 0 for Simple Legacy Formats, 1 for XML File Format
    Data<defaulttype::Vec3Types::VecCoord> position; ///< points position (will use points from topology or mechanical state if this is empty)
    Data<bool> writeEdges; ///< write edge topology
    Data<bool> writeTriangles; ///< write triangle topology
    Data<bool> writeQuads; ///< write quad topology
    Data<bool> writeTetras; ///< write tetra topology
    Data<bool> writeHexas; ///< write hexa topology
    Data<helper::vector<std::string> > dPointsDataFields; ///< Data to visualize (on points)
    Data<helper::vector<std::string> > dCellsDataFields; ///< Data to visualize (on cells)
    Data<unsigned int> exportEveryNbSteps; ///< export file only at specified number of steps (0=disable)
    Data<bool> exportAtBegin; ///< export file at the initialization
    Data<bool> exportAtEnd; ///< export file when the simulation is finished
    Data<bool> overwrite; ///< overwrite the file, otherwise create a new file at each export, with suffix in the filename

    int nbFiles;
    int sigmaPointIndex;

    double lastTime;

    helper::vector<std::string> pointsDataObject;
    helper::vector<std::string> pointsDataField;
    helper::vector<std::string> pointsDataName;

    helper::vector<std::string> cellsDataObject;
    helper::vector<std::string> cellsDataField;
    helper::vector<std::string> cellsDataName;
protected:
    SigmaPointsVTKExporter();
    virtual ~SigmaPointsVTKExporter();
public:
    void init() override;
    void cleanup() override;
    void bwdInit() override;

    void handleEvent(sofa::core::objectmodel::Event *) override;
};



} // namespace misc

} // namespace component

} // namespace sofa

